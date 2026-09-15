import { app } from "../../scripts/app.js";

const IMAGE_COUNT_MIN = 1;
const IMAGE_COUNT_MAX = 5;
const IMAGE_WIDGET_NAMES = [
  "image",
  "mask",
  "alpha",
  "mask_blur",
  "mask_strength",
  "mode",
];

const handledNodes = new WeakSet();

const findWidgetByName = (node, name) =>
  node.widgets?.find((widget) => widget.name === name);

const getNodeType = (node) =>
  node?.constructor?.comfyClass ?? node?.comfyClass ?? node?.type;

/**
 * ComfyUI uses widget.hidden for LiteGraph layout and rendering visibility.
 * The same property is also consumed by the Node 2.0 renderer.
 */
function setWidgetHidden(widget, hidden) {
  if (!widget) return false;

  const changed = widget.hidden !== hidden;
  widget.hidden = hidden;
  return changed;
}

function updateNodeLayout(node) {
  if (
    typeof node.computeSize !== "function" ||
    typeof node.setSize !== "function"
  ) {
    return;
  }

  const newSize = node.computeSize();
  if (!newSize || !node.size) return;

  node.setSize([node.size[0], newSize[1]]);
  app.canvas?.setDirty?.(true, true);
}

function getImageCount(value) {
  const count = Number(value);
  if (!Number.isFinite(count)) return IMAGE_COUNT_MIN;

  return Math.max(
    IMAGE_COUNT_MIN,
    Math.min(IMAGE_COUNT_MAX, Math.floor(count)),
  );
}

function updateImageWidgetsVisibility(node, value) {
  const imageCount = getImageCount(value);
  let changed = false;

  for (let index = 1; index <= IMAGE_COUNT_MAX; index += 1) {
    const hidden = index > imageCount;

    for (const baseName of IMAGE_WIDGET_NAMES) {
      changed =
        setWidgetHidden(
          findWidgetByName(node, `${baseName}_${index}`),
          hidden,
        ) || changed;
    }
  }

  if (changed) updateNodeLayout(node);
}

function attachWidgetCallback(widget, onChange) {
  const originalCallback = widget.callback;

  widget.callback = function (...args) {
    let result;
    try {
      result = originalCallback?.apply(this, args);
    } finally {
      onChange(args[0] ?? widget.value);
    }
    return result;
  };
}

app.registerExtension({
  name: "hakuimg.blend.widgethider",
  nodeCreated(node) {
    if (getNodeType(node) !== "BlendImage") return;

    const countWidget = findWidgetByName(node, "images_count");
    if (!countWidget || handledNodes.has(node)) return;

    handledNodes.add(node);

    const syncVisibility = (value = countWidget.value) => {
      updateImageWidgetsVisibility(node, value);
    };

    attachWidgetCallback(countWidget, syncVisibility);

    const originalOnWidgetChanged = node.onWidgetChanged;
    node.onWidgetChanged = function (name, value, ...args) {
      const result = originalOnWidgetChanged?.call(this, name, value, ...args);
      if (name === "images_count") syncVisibility(value);
      return result;
    };

    const originalOnAfterGraphConfigured = node.onAfterGraphConfigured;
    node.onAfterGraphConfigured = function (...args) {
      const result = originalOnAfterGraphConfigured?.apply(this, args);
      syncVisibility();
      return result;
    };

    syncVisibility();
  }
});
