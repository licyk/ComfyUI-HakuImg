// revise from https://github.com/jags111/efficiency-nodes-comfyui/blob/main/js/widgethider.js
import { app } from "../../scripts/app.js";

let origProps = {};

const findWidgetByName = (node, name) => {
  return node.widgets ? node.widgets.find((w) => w.name === name) : null;
};

const doesInputWithNameExist = (node, name) => {
  return node.inputs ? node.inputs.some((input) => input.name === name) : false;
};

const HIDDEN_TAG = "tschide";

function toggleWidget(node, widget, show = false, suffix = "") {
  if (!widget || doesInputWithNameExist(node, widget.name)) return;

  if (!origProps[widget.name]) {
    origProps[widget.name] = {
      origType: widget.type,
      origComputeSize: widget.computeSize,
    };
  }

  widget.type = show ? origProps[widget.name].origType : HIDDEN_TAG + suffix;
  widget.computeSize = show
    ? origProps[widget.name].origComputeSize
    : () => [0, -4];
  widget.linkedWidgets?.forEach((w) =>
    toggleWidget(node, w, ":" + widget.name, show)
  );

  const newHeight = node.computeSize()[1];

  node.setSize([node.size[0], newHeight]);
}

function handleVisibility(node, countValue, node_type) {
  const baseNamesMap = {
    image: ["image", "mask", "alpha", "mask_blur", "mask_strength", "mode"],
  };

  const baseNames = baseNamesMap[node_type];

  for (let i = 1; i <= 50; i++) {
    const nameWidget = findWidgetByName(node, `${baseNames[0]}_${i}`);
    const firstWidget = findWidgetByName(node, `${baseNames[1]}_${i}`);
    const secondWidget = findWidgetByName(node, `${baseNames[2]}_${i}`);
    const thirdWidget = findWidgetByName(node, `${baseNames[3]}_${i}`);
    const fourthWidget = findWidgetByName(node, `${baseNames[4]}_${i}`);
    const fifthWidget = findWidgetByName(node, `${baseNames[5]}_${i}`);

    if (i <= countValue) {
      toggleWidget(node, nameWidget, true);
      toggleWidget(node, firstWidget, true);
      toggleWidget(node, secondWidget, true);
      toggleWidget(node, thirdWidget, true);
      toggleWidget(node, fourthWidget, true);
      toggleWidget(node, fifthWidget, true);
    } else {
      toggleWidget(node, nameWidget, false);
      toggleWidget(node, firstWidget, false);
      toggleWidget(node, secondWidget, false);
      toggleWidget(node, thirdWidget, false);
      toggleWidget(node, fourthWidget, false);
      toggleWidget(node, fifthWidget, false);
    }
  }
}

const nodeWidgetHandlers = {
  BlendImage: {
    images_count: handleimage,
  },
};

function widgetLogic(node, widget) {
  const handler = nodeWidgetHandlers[node.comfyClass]?.[widget.name];

  if (handler) {
    handler(node, widget);
  }
}

function handleimage(node, widget) {
  handleVisibility(node, widget.value, "image");
}

app.registerExtension({
  name: "hakuimg.blend.widgethider",
  nodeCreated(node) {
    for (const w of node.widgets || []) {
      let widgetValue = w.value;
      let originalDescriptor = Object.getOwnPropertyDescriptor(w, "value");
      if (!originalDescriptor) {
        originalDescriptor = Object.getOwnPropertyDescriptor(
          w.constructor.prototype,
          "value"
        );
      }
      widgetLogic(node, w);
      Object.defineProperty(w, "value", {
        get() {
          let valueToReturn =
            originalDescriptor && originalDescriptor.get
              ? originalDescriptor.get.call(w)
              : widgetValue;

          return valueToReturn;
        },
        set(newVal) {
          if (originalDescriptor && originalDescriptor.set) {
            originalDescriptor.set.call(w, newVal);
          } else {
            widgetValue = newVal;
          }
          widgetLogic(node, w);
        },
      });
    }
    setTimeout(() => {
      initialized = true;
    }, 500);
    // alert("hakuimg test");
  },
});
