import React from "react";

const Hero = () => {
  return (
    <header className={"container mx-auto rounded-lg overflow-hidden"}>
      <div
        className="w-full bg-center bg-cover h-[38rem]"
        style={{
          backgroundImage:
            "url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NzN8fG9ubGluZXxlbnwwfHwwfHx8MA%3D%3D')",
        }}
      >
        <div className="flex gap-4 items-center pl-[150px] h-full bg-gray-900/60">
          <div className="">
            <h1 className="font-semibold text-white lg:text-5xl">
              The Future of <span className="text-blue-300">Media</span> is
              Collaborative
            </h1>
            <p className={"text-white/60 max-w-[950px] mt-2"}>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam
              tincidunt efficitur ante, nec imperdiet eros sodales id.
              Pellentesque sit amet enim sapien. Nunc odio nunc.{" "}
            </p>
            <button className="w-full px-8 py-3 mt-4 text-sm font-medium text-white capitalize transition-colors duration-300 transform bg-blue-700 rounded-md lg:w-auto hover:bg-blue-500 focus:outline-none focus:bg-blue-500">
              Get Started
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Hero;
