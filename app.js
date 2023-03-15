//setup for the rest of the node app
const path = require("path");
const express = require("express");
const { engine } = require("express-handlebars");
const { spawn } = require("child_process");
const PORT = 8111;
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.resolve(__dirname, "public")));
app.engine(
  ".hbs",
  engine({
    extname: ".hbs",
    helpers: {
      json: (context) => JSON.stringify(context),
    },
  })
);
app.set("view engine", ".hbs");
var helpers = require("handlebars-helpers")();
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: false });


app.get("/", (req, res) => {
  res.render("index");
});

//combined with post method to retrieve data from the form, send to 
//python microservice, take json from python and display in a table
app.get("/main", (req, res) => {
  res.sendFile(__dirname + "/views/layouts/main.hbs");
});
app.post("/", urlencodedParser, (req, res) => {
  //timeSpan is int, keyword is string  
  const timeSpan = req.body.search_range;
  const keyword = req.body.keyword;
  const pythonScript = spawn("python", ["pubmed.py", keyword, timeSpan]);
  let data = "";

  pythonScript.stdout.on("data", (chunk) => {
    data += chunk.toString();
  });

  pythonScript.on("close", (code) => {
    if (code !== 0) {
      res.send(`Something went  wrong. Exit code: ${code}`);
      return;
    }

    const collected_articles = JSON.parse(data);
    res.render("results", { keyres: keyword, jjson: collected_articles });
  });
});

app.get("/results", (req, res) => {
  res.render("results");
});









app.listen(PORT, () => {
  console.log(
    `Express started on http://localhost:${PORT}`
  );
});
