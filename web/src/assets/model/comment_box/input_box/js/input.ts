// 递归应用样式到span标签，处理嵌套的span标签
function applyStyleToNestedSpans(span: HTMLElement, styles: { [key: string]: string | null }): void {
    // 遍历传入的样式键值对，设置样式
    Object.entries(styles).forEach(([key, value]) => {
        if (value !== null) {
            const styleValue = span.style[key as any];
            // 如果样式已存在且与当前样式相同，移除该样式
            if (styleValue === value) {
                span.style[key as any] = "";
            } else {
                // 忽略黄色背景色
                if (key === "backgroundColor" && value === "yellow") {
                    return;
                }
                span.style[key as any] = value;
            }
        }
    });

    // 如果存在嵌套的span标签，也递归应用样式
    Array.from(span.children).forEach(child => {
        if (child instanceof HTMLSpanElement) {
            applyStyleToNestedSpans(child, styles);  // 递归处理嵌套的span标签
        }
    });
}

// 通过id获取span元素，并根据传入的样式设置样式
function set_span_style(styles: { [key: string]: string | null }) {
    const span = document.getElementById("tempValue");
    if (span) {
        applyStyleToNestedSpans(span, styles);  // 调用递归函数应用样式
        span.removeAttribute("id"); // 设置完成后去掉id属性
    }
}

// 清除指定 ref 对象中的所有 span 标签的样式
function clear_all_span_style_in_ref(ref: HTMLElement) {
    // 获取 ref 对象中的所有 span 标签
    const spans = ref.querySelectorAll("span");

    // 遍历所有 span 标签并清除样式
    spans.forEach(span => {
        span.style.color = "";
        span.style.fontSize = "";
        span.style.fontWeight = "";
        span.style.fontStyle = "";
        span.style.textDecoration = "";
        span.style.backgroundColor = "";
        span.style.fontFamily = "";
        span.style.verticalAlign = "";
        span.style.letterSpacing = "";
        span.style.lineHeight = "";
        span.style.textAlign = "";
        span.style.textIndent = "";
        span.style.textShadow = "";
    });
}

//通过<span id="tempValue">来模拟选中的文字，需要跳过img标签
function getSelectedText(el: HTMLElement) {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);

    // 验证选区是否在目标元素内
    if (!el.contains(range.commonAncestorContainer)) {
        return;
    }

    // 检查并移除已有的 tempValue 节点
    const existingTempSpan = el.querySelector("#tempValue");
    if (existingTempSpan) {
        const parent = existingTempSpan.parentNode;
        if (parent) {
            while (existingTempSpan.firstChild) {
                parent.insertBefore(existingTempSpan.firstChild, existingTempSpan);
            }
            parent.removeChild(existingTempSpan);
        }
    }

    // 创建临时容器
    const tempSpan = document.createElement("span");
    tempSpan.id = "tempValue";
    tempSpan.style.backgroundColor = "yellow";

    // 提取选区内容并用 <span> 包裹
    const extractedContent = range.extractContents();
    tempSpan.appendChild(extractedContent);
    range.insertNode(tempSpan);

    // 获取选中的文本
    const selectedText = tempSpan.textContent;

    // 恢复原始选区
    selection.removeAllRanges();
    const newRange = document.createRange();
    newRange.selectNodeContents(tempSpan);
    selection.addRange(newRange);

    return selectedText;
}

//点击指定位置之外的地方时，移除选中的文字,解包span
function removeSelectedText(e: HTMLElement) {
    const tempSpan = e.querySelector("#tempValue");
    if (tempSpan) {
        const parent = tempSpan.parentNode;
        if (parent) {
            while (tempSpan.firstChild) {
                parent.insertBefore(tempSpan.firstChild, tempSpan);
            }
            parent.removeChild(tempSpan);
        }
    }
}

// 将光标放到内容的末尾
function placeCaretAtEnd(el: HTMLElement) {
    el.focus();
    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    const sel = window.getSelection();
    if (sel) {
        sel.removeAllRanges();
        sel.addRange(range);
    }
}

//生成唯一ID
function generateUniqueId() {
    //生成一个唯一的UUID
    const uuid= 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
    return uuid;
}

export {
    placeCaretAtEnd,
    getSelectedText,
    removeSelectedText,
    set_span_style,
    clear_all_span_style_in_ref,
    generateUniqueId
};
