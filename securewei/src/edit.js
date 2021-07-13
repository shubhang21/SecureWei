import React from 'react';
import AceEditor from 'react-ace';

const edit=(props)=>{

    function onChange(newValue) {
        th
        console.log("change", newValue);
      }
      
    

    return (
        <AceEditor  mode="javascript" width="100%" height="100%" showPrintMargin={false} theme="monokai" onChange={onChange}
    name="UNIQUE_ID_OF_DIV"
    editorProps={{ $blockScrolling: true }}
    setOptions={{
      enableBasicAutocompletion: true,
      enableLiveAutocompletion: true,
      enableSnippets: true,
      useWorker: false
            }}/>
    );

}

export default edit;
