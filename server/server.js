import express from "express";
import cors from "cors";
import records from "./routes/records.js";

const PORT = process.env.PORT || 5050;
const app = express();

app.use(cors());
app.use(express.json());
app.use("/record", records);

// start the express server
app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
})

//mongodb+srv://doorbell:6ZbZ6ghK88CNxyQt_@@doorbell.duv9kmk.mongodb.net/?retryWrites=true&w=majority&appName=Doorbell