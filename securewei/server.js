const { createServer } = require("http");





const express = require("express");
const compression = require("compression");
const morgan = require("morgan");
const path = require("path");
const normalizePort= port => parseInt(port,10)
const PORT =normalizePort(process.env.PORT||5000)
var cors = require("cors");
const bodyParser = require("body-parser");
var app = express();
var fs = require('fs');

const dev= app.get('env')!=='production'
if(!dev)
{
    app.disable('x-powered-by')
    app.use(compression())
    app.use(morgan('common'))
    app.use(express.static(path.resolve(__dirname,'build')))
    app.get('*',(req,res)=>{
        res.sendFile(path.resolve(__dirname,'build','index.html')
        )
        
    })
}
if(dev)
{
    app.use(morgan('dev'))
}
const server = createServer(app)
server.listen(PORT,err=>{
    if(err)throw err

    console.log('Server Started')
})

app.use(cors());
app.options("*", cors()); // enable pre-flight
app.use(bodyParser.json());

let { PythonShell } = require("python-shell");
const { normalize } = require("path");

var code = " hello variable";
app.get("/hello", (req, res) => {
  res.send("hello there");
  console.log("helloo");
});

app.get("/api", (req, res) => {
//   const input = req.query.code.split(",");
  console.log(req.query.code);
  //Here are the option object in which arguments can be passed for the python_test.js.
  let options = {
    mode: "text",
    pythonOptions: ["-u"], // get print results in real-time
    args: [req.query.code], //An argument which can be accessed in the script using sys.argv[1]
  };

  PythonShell.run("main.py", options, function (err, result) {
    if (err) throw err;
    // result is an array consisting of messages collected
    //during execution of script.
    // console.log(result);
    // const r = result&&result.toString();
    // const re = r&&r.split(",");
//     var obj = require('./SLITHER-ANALYSIS.json');
    
// console.log(result)
// console.log(obj)

res.send( [].concat(result || []))
    
  });
});
// console.log(obj)
// Creates a server which runs on port 3000 and
// can be accessed through localhost:3000

