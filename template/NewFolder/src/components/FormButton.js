import React from 'react';
import Button from './Button';
function FormButton({
    isEditing,
    submitCount,
    onAddOrUpdate,
    onCancel,
    onGenerate,
    onCopy,
    showGenerated,
    copyStatus,
}){
return(
    <div>
        <Button type="submit" onClick={onAddOrUpdate} >
            {isEditing? 'Update' : `Add(${submitCount})`}
        </Button>

        {isEditing && (
            <Button onClick={onCancel} style={{marginLeft:10,backgroundColor:'#ccc'}}>Cancel</Button>
        )}

        <Button onClick={onGenerate}>Generate</Button>
        {showGenerated && (
            <>
            <Button onClick={onCopy}>Copy to Clipboard</Button>
            {copyStatus && <span style={{marginLeft:10}}>{copyStatus}</span>}
            </>
        )}

        <Button onClick={() => {
                const confirmDelete = window.confirm("Are you sure you want to delete this item?");
                if (confirmDelete) {
                  const updatedList = [...submit];
                  updatedList.splice(index, 1); 
                  const reordered = reassignOrderIds(updatedList);
                  setSubmit(reordered);}}}>Delete</Button>

    </div>
)
}
export default FormButton;
