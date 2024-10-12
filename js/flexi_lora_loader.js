import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "FlexiLoRALoader",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "FlexiLoRALoader") {
            // ドロップダウンメニューの実装など
            const onCreate = nodeType.prototype.onCreate;
            nodeType.prototype.onCreate = function() {
                onCreate?.apply(this, arguments);
                // ここにUIの拡張ロジックを実装
            }
        }
    }
});