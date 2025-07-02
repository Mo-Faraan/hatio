import { useState } from "react";
import Button from "./Button";

export default function CopyButton({ text, onCopyStatus }) {
  const [localStatus, setLocalStatus] = useState("");

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      const message = "Copied!";
      if (onCopyStatus) onCopyStatus(message);
      else setLocalStatus(message);

      setTimeout(() => {
        if (onCopyStatus) onCopyStatus("");
        else setLocalStatus("");
      }, 2000);
    } catch {
      const message = "Failed to copy";
      if (onCopyStatus) onCopyStatus(message);
      else setLocalStatus(message);
    }
  };

  return (
    <>
      <Button onClick={handleCopy}>Copy to Clipboard</Button>
      {!onCopyStatus && localStatus && (
        <span style={{ marginLeft: "10px" }}>{localStatus}</span>
      )}
    </>
  );
}
