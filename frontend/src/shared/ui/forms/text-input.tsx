import { InputProps } from "./types";

export function UITextInput({
  label,
  errorMsg,
  className,
  ...inputProps
}: InputProps) {
  const hasError = !!errorMsg;

  return (
    <div className={`w-full ${className || ""}`}>
      <div className="relative">
        <input
          {...inputProps}
          id={label}
          className={`
            peer w-full px-3 pt-6 pb-2 border rounded-md
            bg-transparent placeholder-transparent
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            transition-colors duration-200
            ${hasError
              ? "border-red-500 focus:ring-red-500 focus:border-red-500"
              : "border-gray-300 hover:border-gray-400"
            }
          `}
          placeholder={label}
        />
        <label
          htmlFor={label}
          className={`
            absolute left-3 top-2 text-xs font-medium transition-all duration-200
            peer-placeholder-shown:text-base peer-placeholder-shown:top-4
            peer-focus:text-xs peer-focus:top-2
            ${hasError ? "text-red-500" : "text-gray-500 peer-focus:text-blue-500"}
          `}
        >
          {label}
        </label>
      </div>
      {errorMsg && (
        <p className="mt-1 text-sm text-red-500">{errorMsg}</p>
      )}
    </div>
  );
}
