import Form from "../components/Form"

function Login() {
    return(
        <div className="relative w-screen h-screen overflow-hidden">
            <img
            src="/images/login-img.jpg"
            alt="Landing"
            className="w-screen h-screen object-cover filter"
            />
            <div className="absolute top-25 left-5 text-white w-200">
                <Form route="/api/token/" method="login" />
            </div>
        </div>
    );
}


export default Login