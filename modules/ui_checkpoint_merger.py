
import gradio as gr

from modules import sd_models, sd_vae, errors, extras, call_queue
from modules.ui_components import FormRow
from modules.ui_common import create_refresh_button


def update_interp_description(value):
    interp_description_css = "<p style='margin-bottom: 2.5em'>{}</p>"
    interp_descriptions = {
        "No interpolation": interp_description_css.format("補間は一切使用しません。1つのモデルが必要です;A. フォーマット変換とVAEベイクが可能です。"),
        "Weighted sum": interp_description_css.format("補間には加重和が用いられます。2つのモデルが必要です。AとB。結果は A * (1 - M) + B * M として計算されます。"),
        "Add difference": interp_description_css.format("最後の2つのモデルの差が最初のモデルに加えられます。3つのモデルが必要です; A, B, C。結果は A + (B - C) * M として計算されます。")
    }
    return interp_descriptions[value]


def modelmerger(*args):
    try:
        results = extras.run_modelmerger(*args)
    except Exception as e:
        errors.report("Error loading/saving model file", exc_info=True)
        sd_models.list_models()  # to remove the potentially missing models from the list
        return [*[gr.Dropdown.update(choices=sd_models.checkpoint_tiles()) for _ in range(4)], f"Error merging checkpoints: {e}"]
    return results


class UiCheckpointMerger:
    def __init__(self):
        with gr.Blocks(analytics_enabled=False) as modelmerger_interface:
            with gr.Row(equal_height=False):
                with gr.Column(variant='compact'):
                    self.interp_description = gr.HTML(value=update_interp_description("Weighted sum"), elem_id="modelmerger_interp_description")

                    with FormRow(elem_id="modelmerger_models"):
                        self.primary_model_name = gr.Dropdown(sd_models.checkpoint_tiles(), elem_id="modelmerger_primary_model_name", label="プライマリーモデル(A)")
                        create_refresh_button(self.primary_model_name, sd_models.list_models, lambda: {"choices": sd_models.checkpoint_tiles()}, "refresh_checkpoint_A")

                        self.secondary_model_name = gr.Dropdown(sd_models.checkpoint_tiles(), elem_id="modelmerger_secondary_model_name", label="セカンダリーモデル(B)")
                        create_refresh_button(self.secondary_model_name, sd_models.list_models, lambda: {"choices": sd_models.checkpoint_tiles()}, "refresh_checkpoint_B")

                        self.tertiary_model_name = gr.Dropdown(sd_models.checkpoint_tiles(), elem_id="modelmerger_tertiary_model_name", label="三次モデル(C)")
                        create_refresh_button(self.tertiary_model_name, sd_models.list_models, lambda: {"choices": sd_models.checkpoint_tiles()}, "refresh_checkpoint_C")

                    self.custom_name = gr.Textbox(label="カスタムネーム(オプション)", elem_id="modelmerger_custom_name")
                    self.interp_amount = gr.Slider(minimum=0.0, maximum=1.0, step=0.05, label='乗数(M) - モデルAを得るために0に設定', value=0.3, elem_id="modelmerger_interp_amount")
                    self.interp_method = gr.Radio(choices=["No interpolation", "Weighted sum", "Add difference"], value="Weighted sum", label="補間法", elem_id="modelmerger_interp_method")
                    self.interp_method.change(fn=update_interp_description, inputs=[self.interp_method], outputs=[self.interp_description])

                    with FormRow():
                        self.checkpoint_format = gr.Radio(choices=["ckpt", "safetensors"], value="safetensors", label="チェックポイント形式", elem_id="modelmerger_checkpoint_format")
                        self.save_as_half = gr.Checkbox(value=False, label="float16として保存", elem_id="modelmerger_save_as_half")

                    with FormRow():
                        with gr.Column():
                            self.config_source = gr.Radio(choices=["A, B or C", "B", "C", "Don't"], value="A, B or C", label="設定のコピー元", type="index", elem_id="modelmerger_config_method")

                        with gr.Column():
                            with FormRow():
                                self.bake_in_vae = gr.Dropdown(choices=["None"] + list(sd_vae.vae_dict), value="None", label="VAEを埋め込む", elem_id="modelmerger_bake_in_vae")
                                create_refresh_button(self.bake_in_vae, sd_vae.refresh_vae_list, lambda: {"choices": ["None"] + list(sd_vae.vae_dict)}, "modelmerger_refresh_bake_in_vae")

                    with FormRow():
                        self.discard_weights = gr.Textbox(value="", label="一致する名前の重みを破棄", elem_id="modelmerger_discard_weights")

                    with gr.Accordion("Metadata", open=False) as metadata_editor:
                        with FormRow():
                            self.save_metadata = gr.Checkbox(value=True, label="メタデータを保存", elem_id="modelmerger_save_metadata")
                            self.add_merge_recipe = gr.Checkbox(value=True, label="マージレシピのメタデータを追加", elem_id="modelmerger_add_recipe")
                            self.copy_metadata_fields = gr.Checkbox(value=True, label="マージされたモデルからメタデータをコピー", elem_id="modelmerger_copy_metadata")

                        self.metadata_json = gr.TextArea('{}', label="JSON形式のメタデータ")
                        self.read_metadata = gr.Button("選択されたチェックポイントからメタデータを読み込む")

                    with FormRow():
                        self.modelmerger_merge = gr.Button(elem_id="modelmerger_merge", value="Merge", variant='primary')

                with gr.Column(variant='compact', elem_id="modelmerger_results_container"):
                    with gr.Group(elem_id="modelmerger_results_panel"):
                        self.modelmerger_result = gr.HTML(elem_id="modelmerger_result", show_label=False)

        self.metadata_editor = metadata_editor
        self.blocks = modelmerger_interface

    def setup_ui(self, dummy_component, sd_model_checkpoint_component):
        self.checkpoint_format.change(lambda fmt: gr.update(visible=fmt == 'safetensors'), inputs=[self.checkpoint_format], outputs=[self.metadata_editor], show_progress=False)

        self.read_metadata.click(extras.read_metadata, inputs=[self.primary_model_name, self.secondary_model_name, self.tertiary_model_name], outputs=[self.metadata_json])

        self.modelmerger_merge.click(fn=lambda: '', inputs=[], outputs=[self.modelmerger_result])
        self.modelmerger_merge.click(
            fn=call_queue.wrap_gradio_gpu_call(modelmerger, extra_outputs=lambda: [gr.update() for _ in range(4)]),
            _js='modelmerger',
            inputs=[
                dummy_component,
                self.primary_model_name,
                self.secondary_model_name,
                self.tertiary_model_name,
                self.interp_method,
                self.interp_amount,
                self.save_as_half,
                self.custom_name,
                self.checkpoint_format,
                self.config_source,
                self.bake_in_vae,
                self.discard_weights,
                self.save_metadata,
                self.add_merge_recipe,
                self.copy_metadata_fields,
                self.metadata_json,
            ],
            outputs=[
                self.primary_model_name,
                self.secondary_model_name,
                self.tertiary_model_name,
                sd_model_checkpoint_component,
                self.modelmerger_result,
            ]
        )

        # Required as a workaround for change() event not triggering when loading values from ui-config.json
        self.interp_description.value = update_interp_description(self.interp_method.value)

