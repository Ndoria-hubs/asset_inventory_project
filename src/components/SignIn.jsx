// import { react } from react

const SignIn = () => {
    const handleSignClick = () => {
        // if pass direct to dashboard/main else reject
        pass
    }

    return (
        <div>
            <h1>Welcome back . Sign in to continue</h1>
            <div>
                <label>
                    Username
                </label>
                <input placeholder="username"></input>
                <label>
                    Password
                </label>
                <input placeholder="password"></input>
                <button onClick={handleSignClick}>Sign in</button>
            </div>
        </div>
    )
}

export default SignIn