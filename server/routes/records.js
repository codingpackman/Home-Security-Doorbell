import express from "express";

// This will help us connect to the database
import db from "../database/connection.js";

// This helps convert the id from string to ObjectId for the _id
import { ObjectId } from "mongodb";

// Import authentication middleware
import { generateToken, verifyToken } from "../middleware/auth.js";
import bcrypt from "bcryptjs";

// Routes is an instance of the express router
const router = express.Router();

// This section will help you get a list of all the records (protected route)
router.get("/", verifyToken, async (req, res) => {
    try {
        const collection = db.collection("records");
        const results = await collection.find({}).toArray();
        res.status(200).send(results);
    } catch (err) {
        console.error(err);
        res.status(500).send("Error fetching records");
    }
});

// Get current logged-in user information route
router.get("/me", verifyToken, async (req, res) => {
    try {
        const collection = db.collection("records");
        const user = await collection.findOne({ _id: new ObjectId(req.user.userId) });
        
        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }

        // Don't return password
        const { password, ...userWithoutPassword } = user;
        res.status(200).json(userWithoutPassword);
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Error fetching user information" });
    }
});

// This section will help you get a single record by id
router.get("/:id", async (req, res) => {
    try {
        const collection = db.collection("records");
        const query = { _id: new ObjectId(req.params.id) };
        const result = await collection.findOne(query);

        if (!result) {
            res.status(404).send("Not found");
        } else {
            res.status(200).send(result);
        }
    } catch (err) {
        console.error(err);
        res.status(500).send("Error fetching record");
    }
});

// This section will help you create a new record
router.post("/", async (req, res) => {
    try {
        const { username, password, doorbellID } = req.body;

        // Check if username already exists
        const collection = db.collection("records");
        const existingUser = await collection.findOne({ username });
        
        if (existingUser) {
            return res.status(400).json({ message: "Username already exists" });
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);

        const newDocument = {
            username: username,
            password: hashedPassword,
            doorbellID: doorbellID,
            createdAt: new Date()
        };

        const result = await collection.insertOne(newDocument);

        // Generate JWT token
        const token = generateToken(result.insertedId.toString(), username, doorbellID);

        // Return success response with token
        res.status(201).json({
            message: "Account created successfully",
            token: token,
            user: {
                id: result.insertedId,
                username: username,
                doorbellID: doorbellID
            }
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Error adding record" });
    }
});

// This section will help you update a record by id
router.patch("/:id", async (req, res) => {
    try {
        const query = { _id: new ObjectId(req.params.id) };
        const updates = {
            $set: {
                username: req.body.username,
                password: req.body.password,
                doorbellID: req.body.doorbellID,
            },
        };

        const collection = db.collection("records");
        const result = await collection.updateOne(query, updates);

        res.status(200).send(result);
    } catch (err) {
        console.error(err);
        res.status(500).send("Error updating record");
    }
});

// This section will help you delete a record
router.delete("/:id", async (req, res) => {
    try {
        const query = { _id: new ObjectId(req.params.id) };

        const collection = db.collection("records");
        const result = await collection.deleteOne(query);

        res.status(200).send(result);
    } catch (err) {
        console.error(err);
        res.status(500).send("Error deleting record");
    }
});

//This section will check if login credentials are correct
router.post("/login", async (req, res) => {
    try {
        const { username, password } = req.body;

        const collection = db.collection("records");
        const user = await collection.findOne({ username });

        if (!user) {
            return res.status(401).json({ message: "Invalid username or password" });
        }

        // Check password - supports both old plaintext and new encrypted passwords
        let isPasswordValid = false;
        
        if (user.password.startsWith('$2a$') || user.password.startsWith('$2b$')) {
            // Encrypted password
            isPasswordValid = await bcrypt.compare(password, user.password);
        } else {
            // Old plaintext password (for backward compatibility)
            isPasswordValid = password === user.password;
        }

        if (!isPasswordValid) {
            return res.status(401).json({ message: "Invalid username or password" });
        }

        // Generate JWT token
        const token = generateToken(user._id.toString(), user.username, user.doorbellID);

        // Return success response with token
        res.status(200).json({
            message: "Login successful",
            token: token,
            user: {
                id: user._id,
                username: user.username,
                doorbellID: user.doorbellID
            }
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: "Error during login" });
    }
});

export default router;