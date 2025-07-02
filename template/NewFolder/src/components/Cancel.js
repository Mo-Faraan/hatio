import Button from "./Button";

export default function CancelButton({ onCancel }) {
  return (
    <Button
      onClick={onCancel}
      style={{ marginLeft: "10px", backgroundColor: "#ccc" }}
    >
      Cancel
    </Button>
  );
}   

