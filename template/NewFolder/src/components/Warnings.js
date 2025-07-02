import { useEffect } from "react";

export default function useNavigationWarning(hasUnsavedData, hasCopied) {
  useEffect(() => {
    const handleBeforeUnload = (e) => {
      if (hasUnsavedData && !hasCopied) {
        e.preventDefault();
        e.returnValue = "You haven't copied your data. Are you sure you want to leave?";
      }
    };

    const handlePopState = () => {
      if (hasUnsavedData && !hasCopied) {
        const confirmLeave = window.confirm(
          "You haven't copied your data. Are you sure you want to go back?"
        );
        if (!confirmLeave) {
          window.history.pushState(null, "", window.location.pathname);
        }
      }
    };

    // Add tab close/reload warning
    window.addEventListener("beforeunload", handleBeforeUnload);

    // Push current page to history and handle back button
    window.history.pushState(null, "", window.location.pathname);
    window.addEventListener("popstate", handlePopState);

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
      window.removeEventListener("popstate", handlePopState);
    };
  }, [hasUnsavedData, hasCopied]);
}
