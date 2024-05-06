import httpClient from "@/src/httpclient";
import { useState } from "react";

function LoginPage(){
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const logInUser = async () => {
    console.log(email, password);

    try {
      const resp = await httpClient.post("//localhost:5000/login", {
        email,
        password,
      });

      window.location.href = "/";
    } catch (error: any) {
      if (error.response.status === 401) {
        alert("Invalid credentials");
      }
    }
  }
};