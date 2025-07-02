import Button from "./Button";

export default function DeleteButton({ onDelete }) {
  const handleDelete = () => {
    const confirmDelete = window.confirm("Are you sure you want to delete this item?");
    if (confirmDelete) {
      onDelete();
    }
  };

  return (
    <Button onClick={handleDelete} style={{ marginLeft: "10px", color: "red" }}>
      Delete
    </Button>
  );
}
