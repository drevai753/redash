import React, { useMemo } from "react";
import { maxBy } from "lodash";
import Select, { SelectProps, LabeledValue } from "antd/lib/select";
import { calculateTextWidth } from "@/lib/calculateTextWidth";

const MIN_LEN_FOR_VIRTUAL_SCROLL = 400;

interface VirtualScrollLabeledValue extends LabeledValue {
  label: string;
}

interface VirtualScrollSelectProps extends Omit<SelectProps<string>, "optionFilterProp" | "children"> {
  options: Array<VirtualScrollLabeledValue>;
}
function SelectWithVirtualScroll({ options, ...props }: VirtualScrollSelectProps): JSX.Element {
  const dropdownMatchSelectWidth = useMemo<number | boolean>(() => {
    if (options && options.length > MIN_LEN_FOR_VIRTUAL_SCROLL) {
      const largestOpt = maxBy(options, "label.length");

      if (largestOpt) {
        const offset = 40;
        const optionText = largestOpt.label;
        const width = calculateTextWidth(optionText);
        if (width) {
          return width + offset;
        }
      }

      return true;
    }

    return false;
  }, [options]);

  const a = (
    <Select
      dropdownMatchSelectWidth={dropdownMatchSelectWidth}
      options={options}
      optionFilterProp="label" // as this component expects "options" prop
      tagRender={
            function(item) {
                return (<span className="ant-select-selection-item" title={item.label}>
                            <span className="ant-select-selection-item-content">{item.label}</span>
                            <span className="ant-select-selection-item-remove" unselectable="on" aria-hidden="true" style={{userSelect: "none"}} onClick={item.onClose}>
                                <span role="img" aria-label="close" className="anticon anticon-close">
                                    <svg viewBox="64 64 896 896" focusable="false" className="" data-icon="close" width="1em" height="1em" fill="currentColor" aria-hidden="true">
                                        <path d="M563.8 512l262.5-312.9c4.4-5.2.7-13.1-6.1-13.1h-79.8c-4.7 0-9.2 2.1-12.3 5.7L511.6 449.8 295.1 191.7c-3-3.6-7.5-5.7-12.3-5.7H203c-6.8 0-10.5 7.9-6.1 13.1L459.4 512 196.9 824.9A7.95 7.95 0 00203 838h79.8c4.7 0 9.2-2.1 12.3-5.7l216.5-258.1 216.5 258.1c3 3.6 7.5 5.7 12.3 5.7h79.8c6.8 0 10.5-7.9 6.1-13.1L563.8 512z"></path>
                                    </svg>
                                </span>
                            </span>
                        </span>);
            }
        }
      {...props}
    />
    //{children}
    //</Select>
);
  //window.console.log(a);
  return a;
}

export default SelectWithVirtualScroll;
