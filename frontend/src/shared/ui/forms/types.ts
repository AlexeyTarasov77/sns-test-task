import { DetailedHTMLProps, InputHTMLAttributes } from "react";
import { ComponentType } from "react";
import { ControllerProps } from "react-hook-form";

export interface InputProps extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> {
  label?: string
  errorMsg?: string
  className?: string
}

export interface IFormInputProps extends Omit<ControllerProps<any>, "render"> {
  className?: string;
  label?: string;
  type?: string;
  Component: ComponentType<InputProps>;
}

export type InputSubType = React.FC<
  Omit<IFormInputProps, "Component">
>;

