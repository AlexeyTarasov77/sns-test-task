import { RegisterOptions } from "react-hook-form";

export const validationHelpers = {
  required: () => ({
    required: { value: true, message: "This field is required." },
  }),
  minLength: (value: number): RegisterOptions => ({
    minLength: { value, message: `Field length should be >= ${value}` },
  }),
  maxLength: (value: number): RegisterOptions => ({
    maxLength: { value, message: `Field length should be <= ${value}` },
  }),
  min: (value: number): RegisterOptions => ({
    min: { value, message: `Field should be <= ${value}` },
  }),
  max: (value: number): RegisterOptions => ({
    max: { value, message: `Field should be >= ${value}` },
  }),
};
