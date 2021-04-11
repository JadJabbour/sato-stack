try {
  var expressApp = require("express")();
  var mongoClient = require("mongodb").MongoClient;
  var bodyParser = require("body-parser");

  expressApp.use(bodyParser.json());
  expressApp.use(bodyParser.urlencoded({ extended: true }));

  expressApp.get("/:ticker", (req, res) => {
    mongoClient.connect(
      "mongodb+srv://root:password@127.0.0.1:27017/?authSource=admin",
      function (err, client) {
        if (err) {
          res.status(500).send("An error occured, please try again later");
        } else {
          if (
            !req.query.ticker ||
            req.query.ticker === null ||
            req.query.ticker === ""
          ) {
            res.status(400).send("Invalid or missing ticker symbol");
          }
          try {
            const collection = client
              .db("seersai_curated_predictions")
              .collection(req.query.ticker);
            preds = collection.find().sort({ generated_at: -1 }).limit(1);
            client.close();
            res.status(200).send(preds);
          } catch (e) {
            res
              .status(500)
              .send(
                "Could not connect to DB or collection not found (invalid ticker): " +
                  e.message
              );
          }
        }
      }
    );
  });

  console.log("MongoDB Gateway running on :53385");

  expressApp.listen(8080);
} catch (ex) {
  console.log("There was a problem launching the server");
}
