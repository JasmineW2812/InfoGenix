import "../styles/Style.css";
import { Link } from 'react-router-dom';

function Landing() {
  return (
    <div>
      <div className="relative w-screen h-screen overflow-hidden">
        <img
          src="/images/landing-img.jpg"
          alt="Landing"
          className="w-screen h-screen object-cover filter brightness-[0.65]"
        />

        <div className="flex flex-row gap-10 text-white absolute top-5 right-10 z-20">
            {/* LOGIN */}
            <Link to="/login" className="relative group inline-block cursor-pointer">
                <span className="relative z-10">LOGIN</span>
                <span className="absolute left-1/2 bottom-0 h-[2px] w-0 bg-red-600 transition-all duration-500 transform -translate-x-1/2 group-hover:w-full"></span>
            </Link>

            {/* SIGN UP */}
            <Link to="/register" className="relative group inline-block cursor-pointer">
                <span className="relative z-10">SIGN UP</span>
                <span className="absolute left-1/2 bottom-0 h-[2px] w-0 bg-red-600 transition-all duration-500 transform -translate-x-1/2 group-hover:w-full"></span>
            </Link>
        </div>



        {/* Main Heading + CTA */}
        <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2 flex flex-col items-start gap-10 z-10 text-white px-5">
          <h1 className="text-4xl md:text-6xl font-bold leading-tight">
            <span className="text-red-600 font-extrabold block">Visualise data</span>
            <span className="block">at your fingertips</span>
          </h1>

          <button className="bg-red-400 hover:bg-red-500 rounded-xl px-10 py-3 transition text-white font-semibold text-xl">
            Try now
          </button>
        </div>
      </div>

      {/* How To Section */}
      <div className="w-screen h-[400px] bg-black text-white text-center py-10">
        <h1 className="text-2xl font-semibold mb-10">How to</h1>
        <div className="flex flex-row gap-20 justify-center">
          <div>Step 1</div>
          <div>Step 2</div>
          <div>Step 3</div>
        </div>
      </div>
    </div>
  );
}

export default Landing;
