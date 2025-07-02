
const Button = ({ children, onClick , type ,style = {}}) => {
    const defaultStyle = {
    padding: "5px 10px",
    backgroundColor: "#4CAF50",
    color: "#000",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
    margin: "5px",
    ...style, 
  };
  return (
    <button type={type} onClick={onClick} style={defaultStyle}>
      {children}
    </button>
  );
};
export default Button;

