import React from "react";
import Navbar from "../../components/Navbar";
import Hero from "./Hero";
import BrandsSection from "./BrandsSection";
import Footer from "../../components/Footer";

const HomePage = () => {
  return (
    <div className={"flex flex-col"}>
      <Navbar />
      <Hero />
      <BrandsSection />
      <Footer />
    </div>
  );
};

export default HomePage;
