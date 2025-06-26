import { createPortal } from "react-dom";
import { ClipLoader } from "react-spinners";

export function Loader() {
  const loader = () => (
    <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
      <ClipLoader size={50} color="#0c7ff2" />
    </div>
  )
  return typeof document == "undefined" ? loader() : createPortal(
    loader(),
    document.body,
  );
}
