import { FaInfoCircle } from 'react-icons/fa';
import Button from './Button';
import { template1, template2 } from './Options';

export default function SubmitList({items,pastedIndexes=new Set(),onDelete,onEdit,invalidIndexes = new Set()}){  
  if(!items.length  ) return <p className="text-sm pl-2">No items added yet.</p>
  const allColumn=[...template1,...template2].map(opt => opt.value);
  return(
    <div className="w-full">
      <ul className="list-none p-0">
        {items.map((item, index) => (
          <li
          key={index}
          className={`mb-4 p-4 rounded-md border-black-300  text-sm font-mono overflow-x-auto ${invalidIndexes.has(index) ? "bg-red-100" : "bg-purple-100"}`}
          >
            {pastedIndexes.has(index)&& item.columnName.trim()!=="" && !allColumn.includes(item.columnName) && item.isCustom===false &&(
              <FaInfoCircle
              title="Empty Column Name"
              className="text-blue-600 float-right text-base"
              />
            )
            }
              
            <pre className="whitespace-pre-wrap break-words">{JSON.stringify(item, null, 2)}</pre>
            <div className="flex flex-wrap gap-2 mt-3">
              <Button
              type="button" 
              className={`px-4 py-2 bg-white border-2 border-blue-800 text-blue-800 rounded hover:bg-slate-400`}
              onClick={()=>{onEdit(index)}} >
              Edit
              </Button>  
        
              <Button
              type="button"
              className={`px-4 py-2 bg-white border-2 border-blue-800 text-blue-800 rounded hover:bg-slate-400`}
              onClick={()=>{onDelete(index)}}
              >
              Delete
              </Button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}