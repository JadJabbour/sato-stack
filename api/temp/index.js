try {
  var expressApp = require("express")();
  var mongoClient = require("mongodb").MongoClient;
  var bodyParser = require("body-parser");

  var cors = require('cors')
  
  expressApp.use(cors())
  expressApp.use(bodyParser.json());
  expressApp.use(bodyParser.urlencoded({ extended: true }));

  expressApp.get("/:ticker", (req, res) => {
    mongoClient.connect(
      "mongodb://root:password@mongo:27017/?authSource=admin", { useUnifiedTopology: true },
      function (err, client) {
        if (err) {
          const { name, message } = err
          res.status(500).send({name, message});
        } else {
          if (
            !req.query.ticker ||
            req.query.ticker === null ||
            req.query.ticker === ""
          ) {
            res.status(400).send("Invalid or missing ticker symbol");
          }
          try {
            client
              .db("seers_ai_db")
              .collection('lstm_model')
              .find()
              .toArray((err, docs) => {
                if(req.query.ticker) {
                  docs = docs.filter(i => i['parameters']['ticker'] === req.query.ticker);
                  docs = docs[docs.length-1];
                  client.close();
                  res.status(200).send(docs?.test_predictions[0] || {});
                }
            })
          } catch (e) {
            console.log(
              "Could not connect to DB or collection not found (invalid ticker): " +
              e.message
            );
          }
        }
      }
    );
  });

  console.log("MongoDB Gateway running on :9000");

  expressApp.listen(9000);
} catch (ex) {
  console.log("There was a problem launching the server");
}
