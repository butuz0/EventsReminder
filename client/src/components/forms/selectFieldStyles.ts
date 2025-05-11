import {StylesConfig} from "react-select";

export const selectFieldStyles: StylesConfig = {
  control: (base: any, state: any) => ({
    ...base,
    fontSize: "0.875rem",
    borderRadius: "0.75rem",
    borderColor: state.isFocused ? "#3b82f6" : "#e5e7eb",
    boxShadow: state.isFocused ? "0 0 0 3px #51a2ff" : "none",
    minHeight: "2.25rem"
  }),
  valueContainer: (base) => ({
    ...base,
    padding: "0 0.75rem",
  }),
  placeholder: (base) => ({
    ...base,
    color: "#6a7282",
    fontSize: "0.875rem",
  })
};
