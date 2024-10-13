import { app } from "../../scripts/app.js";

app.registerExtension({
  name: "FlexiLoRALoader",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "FlexiLoRALoader") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        onNodeCreated?.apply(this, arguments);

        const modeInput = this.widgets.find((w) => w.name === "mode");
        const albumNameInput = this.widgets.find((w) => w.name === "album_name");
        const lora1Input = this.widgets.find((w) => w.name === "lora1");
        const lora2Input = this.widgets.find((w) => w.name === "lora2");
        const lora3Input = this.widgets.find((w) => w.name === "lora3");
        const weightsDisplayInput = this.widgets.find((w) => w.name === "weights_display");

        // モードとアルバム名の選択メニューをLoRA1の上に移動
        if (modeInput && albumNameInput && lora1Input) {
          const index = this.widgets.indexOf(lora1Input);
          this.widgets.splice(this.widgets.indexOf(modeInput), 1);
          this.widgets.splice(this.widgets.indexOf(albumNameInput), 1);
          this.widgets.splice(index, 0, modeInput, albumNameInput);
        }

        // 各LoRAの重みとテキスト入力を対応するLoRA選択メニューの直後に配置
        [lora1Input, lora2Input, lora3Input].forEach((loraInput, i) => {
          if (loraInput) {
            const index = this.widgets.indexOf(loraInput);
            const weightInput = this.widgets.find((w) => w.name === `lora${i + 1}_weight`);
            const textInput = this.widgets.find((w) => w.name === `lora${i + 1}_text`);
            if (weightInput && textInput) {
              this.widgets.splice(this.widgets.indexOf(weightInput), 1);
              this.widgets.splice(this.widgets.indexOf(textInput), 1);
              this.widgets.splice(index + 1, 0, weightInput, textInput);
            }
          }
        });

        // weights_displayを最後に移動
        if (weightsDisplayInput) {
          this.widgets.splice(this.widgets.indexOf(weightsDisplayInput), 1);
          this.widgets.push(weightsDisplayInput);
        }
      };
    }
  },
});
