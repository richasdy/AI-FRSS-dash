import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";

// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
const firebaseConfig = {
  apiKey: "AIzaSyABT20ZxTNTzCnFfhc6sPMB7YwnfGQBnpk",
  authDomain: "rfid-de0fd.firebaseapp.com",
  databaseURL: "https://rfid-de0fd-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "rfid-de0fd",
  storageBucket: "rfid-de0fd.firebasestorage.app",
  messagingSenderId: "267435157636",
  appId: "1:267435157636:web:70d97236aa55a3e3333ad1",
  measurementId: "G-CZV8836M51"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Realtime Database and get a reference to the service
export const db = getDatabase(app);
