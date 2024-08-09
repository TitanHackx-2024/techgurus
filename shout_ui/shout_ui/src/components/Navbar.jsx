import React from "react";
import { useNavigate } from "react-router-dom";
const Navbar = () => {
  const navigate = useNavigate();
  return (
    <nav
      className={"w-full py-4 sticky top-0 bg-white/40 backdrop-blur-lg z-10"}
    >
      <div className={"container mx-auto flex justify-between items-center"}>
        <h2>Media</h2>
        <ul className={"flex gap-4"}>
          <li>Product</li>
          <li>Pricing</li>
          <li>Case Studies</li>
          <li>Resources</li>
        </ul>
        <div className={"flex gap-4"}>
          <button
            className={
              "flex justify-center items-center bg-blue-400 px-3 py-2 text-white rounded-lg cursor-pointer hover:bg-blue-500 transition"
            }
            onClick={() => navigate("/register")}
          >
            SignUp
          </button>
          <button
            className={
              "flex justify-center items-center bg-gray-200 px-3 py-2 rounded-lg cursor-pointer hover:bg-gray-300"
            }
            onClick={() => navigate("/register")}
          >
            Login
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
