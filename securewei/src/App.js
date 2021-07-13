import "./App.css";
import React, { useState, useEffect } from "react";
import brace from "brace";
import "brace/mode/javascript";
import "brace/theme/monokai";
import AceEditor from "react-ace";
import { Grid,AppBar,Toolbar,Button,Typography,Box,Table,TableRow,TableBody,TableCell,TableHead } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import SaveList from "./Save";
import swc from './swc.js'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

function App() {
  function onChange(newValue) {
    setcode(newValue);
  }
  const handleSubmit = (e) => {
    if(code=="")
    alert("Please enter code in the input window.")
    else
    console.log(code);
    
    axios.get('http://localhost:5000/api/', {
        params: {
          code: code,
        },
      })
      .then((response) => {
        setdata(response&&response.data)
        setbtnDisabled(false)
      })
      .catch((err) => console.log(err));
  };
  const [data, setdata] = useState(["Click Analyze to check for vulnerabilities","Output will be displayed here"]);
  const [code, setcode] = useState("");
  const [btnDisabled, setbtnDisabled] = useState(true)
  

  const classes = useStyles();
  return (
    <div className="body">
      <Box component="div" display="flex" className="tc">
        <Box
          className="mar"
          component="div"
          style={{ width: "80%", height: "670px" }}
        >
          <div style={{ margin: "0px" }}>
            <AppBar
              position="static"
              color="inherit"
              style={{ backgroundColor: "#343a40" }}              
            >
              <Toolbar >
                <Typography variant="h6" className={classes.title}>
                  <div className="wrapper">
                    <img
                      alt="SecureWei"
                      src="https://www.linkpicture.com/q/imageonline-co-invertedimage.png"
                      type="image"
                      height="35px"
                      width="40px"
                    />{" "}
                    <span style={{marginTop:"10px"}}>SecureWei</span>
                  </div>
                </Typography>
              </Toolbar>
            </AppBar>
          </div>
          <div className="mar" style={{ marginTop: "10px" }}>
            <AceEditor
              mode="javascript"
              width="100%"
              height="400px"
              margin="10px"
              fontSize="14px"
              showPrintMargin={false}
              theme="monokai"
              onChange={onChange}
              name="UNIQUE_ID_OF_DIV"
              editorProps={{ $blockScrolling: true }}
              setOptions={{
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                enableSnippets: true,
                useWorker: false,
              }}
            />
          </div>
          <Box
            className="mar"
            component="div"
            style={{
              height: "200px",
              backgroundColor: "#272822",
              overflowY: "scroll",
            }}
          >
            <AppBar
              position="sticky"
              variant="dense"
              style={{
                height: "50px",
                backgroundColor: "#343a40",
                textAlign: "left",
                
              }}
            >
              <Toolbar variant="dense">
                <Typography variant="h6" className={classes.title} style={{color:"#cfd2da",}} >
                  OUTPUT
                </Typography>
              </Toolbar>
            </AppBar>
            <div style={{ alignContent:"left", textAlign:"left", color:"#FFF",marginLeft:"50px"}}>

             
              <Table>
                <TableBody>
                {data&&console.log(data)}
                
                { data&&data.map((line) => <div><div>{line}</div><br /></div>)
                
                    
               }
              
            </TableBody>
              </Table></div>
            <br></br>
            <p></p>
          </Box>
        </Box>

        <Box className="side mar" component="div" style={{ width: "30%" ,}}>
          <Box style={{overflowY:"scroll",height:"620px"}}>
          <AppBar
            position="sticky"
            color="inherit"
            style={{ backgroundColor: "#272822", marginTop:"0px" }}
            
          >
            <Toolbar >
              <Typography variant="h6" className={classes.title}>
                <div className="wrapcenter">
                 [SWC REGISTRY CODES ]                </div>
              </Typography>
              {/* <Typography variant="h6" className={classes.title}>
           
            <div className="wrapper"><Button variant="contained" color="primary" style={{borderRadius:"50px"}} >Reset</Button></div>
           
           </Typography> */}
            </Toolbar>
          </AppBar>
          <Table >
            <TableHead>
              <TableRow >
                <TableCell style={{color:"#cfd2da"}}>
                  SWC CODE
                </TableCell>
                <TableCell style={{color:"#cfd2da"}}>
                  Vulnerability
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {swc.map(vul=>(<TableRow>
                <TableCell style={{color:"#cfd2da" , border:"black"}} >
                 {vul.code}
                </TableCell>
                <TableCell style={{color:"#cfd2da", border:"black"}}>
                  {vul.Title}
                </TableCell>
              </TableRow>
                 ))}
            </TableBody>
          </Table>
            
          </Box>
          <AppBar
            position="static"
            color="inherit"
            style={{ backgroundColor: "#272822", marginTop:"0px" }}
            
          >
            <Toolbar variant="dense">
              <Typography variant="h6" className={classes.title}>
                <div className="wrapper2">
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleSubmit}
                    style={{ borderRadius: "50px" }}
                  >
                    Analyze
                  </Button>
                  <Button 
                  
                  style={{ borderRadius: "50px" }}
                  variant="contained"
                  color="primary">
                    
                    {(!btnDisabled)&&data?<SaveList list={data} />:<span>Download</span>}
                  </Button>
                </div>
              </Typography>
              
            </Toolbar>
          </AppBar>
          
          
          <Grid container spacing={2}>
            <Grid item>
              <Typography variant="h6" className={classes.title}></Typography>
            </Grid>
          </Grid>
          
        </Box>
        
      </Box>
      
    </div>
  );
}

export default App;
