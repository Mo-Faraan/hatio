import { FaInfoCircle } from 'react-icons/fa';
import Button from './Button';

export default function SubmitList({items,pastedIndexes=new Set(),onDelete,onEdit}){
    
      if(!items.length  ) return <p>No items added yet.</p>
                  
        return(
        <div>
            <ul style={{ padding: 0, listStyleType: "none" }}>
              {items.map((item, index) => (
                        <li
                          key={index}
                          style={{
                            backgroundColor: "#f0f0f0",
                            marginBottom: "10px",
                            padding: "10px",
                            borderRadius: "5px",
                            fontFamily: "monospace",
                          }}
                        >
                          <div>
                             {pastedIndexes.has(index)&&(item.columnName==="" && item.isCustom===true &&(
                                <FaInfoCircle
                                  title="Empty Column Name"
                                  style={{color:"blue",
                                    fontSize: "18px",
                                    top: "10px",
                                    right: "10px",
                                    cursor: "pointer"
                                  }}
                                />
                              ))}
                          </div>
                          <pre>{JSON.stringify(item, null, 2)}</pre>
        
                          <Button
                            type="button" 
                            style={{ backgroundColor: "olive",color: "white" }}
                            onClick={()=>{onEdit(index)}} >
                            Edit
                          </Button>  
        
                          <Button
                            type="button"
                            style={{ marginLeft: "10px",backgroundColor: "red",color: "white" }}
                            onClick={()=>{onDelete(index)}}
                          >
                          Delete
                          </Button>
                        </li>
                      ))}
                    </ul>
                </div>
    )
}