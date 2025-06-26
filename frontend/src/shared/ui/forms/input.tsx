import { Controller } from "react-hook-form";
import { UITextInput } from "./text-input";
import { IFormInputProps, InputSubType } from "./types";

export type InputType = React.FC<IFormInputProps> & {
  Text: InputSubType;
};

export const UIInput: InputType = ({
  name,
  className,
  label,
  type,
  control,
  rules,
  Component,
}: IFormInputProps) => {
  return (
    <Controller
      rules={rules}
      name={name}
      control={control}
      render={({ field: { onChange, value }, fieldState: { error } }) => (
        <Component
          type={type}
          className={className}
          onChange={onChange}
          value={value ?? ""}
          label={label}
          errorMsg={error ? error.message || "Enter a valid value" : undefined}
        />
      )}
    />
  );
};

const textInput: InputSubType = (props) => (
  <UIInput {...props} Component={UITextInput} />)

UIInput.Text = textInput

