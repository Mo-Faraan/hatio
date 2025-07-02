import Button from "./Button";

export default function EditButton({ onEdit }) {
  return (
    <Button onClick={onEdit} style={{ marginRight: "10px", backgroundColor: "#e0e0e0" }}>
      Edit
    </Button>
  );
}
