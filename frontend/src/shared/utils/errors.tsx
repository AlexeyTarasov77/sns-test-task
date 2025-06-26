export const getErrorMessage = (err: unknown) => {
  if (err instanceof Error) return err.message;
  return String(err);
};

export type ErrorMsg = { message?: string } | string;

export const renderError = (err?: ErrorMsg) => {
  if (!err) return null;
  let msg;
  if (typeof err === "string") {
    msg = err;
  } else msg = err.message;
  if (!msg) msg = "Entered invalid value!";
  return <div className="text-red-500 text-lg">{msg}</div>;
};
