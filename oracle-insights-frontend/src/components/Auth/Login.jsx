import React, { useState } from 'react';  
import logoCondor from '../../images/logo_condor.png';  
  
function Login({ onLogin }) {  
  const [username, setUsername] = useState('');  
  const [password, setPassword] = useState('');  
  
  const handleSubmit = (e) => {  
    e.preventDefault();  
    // Aquí va tu lógica de autenticación  
    // Por ahora, llama onLogin() para pasar al dashboard  
    onLogin();  
  };  
  
  return (  
    <div className="h-screen w-screen flex items-center justify-center bg-oracle-dark">  
      <div className="bg-oracle-surface border border-oracle-border rounded-xl p-8 w-full max-w-sm shadow-lg">  
        <div className="flex items-center gap-3 mb-8 justify-center">  
          <img src={logoCondor} alt="Logo" className="h-10 w-auto rounded-full" />  
          <h1 className="text-xl font-semibold text-oracle-text">  
            Ingeniería Condor <span className="text-oracle-accent">Insights</span>  
          </h1>  
        </div>  
  
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">  
          <input  
            type="text"  
            placeholder="Usuario"  
            value={username}  
            onChange={(e) => setUsername(e.target.value)}  
            className="bg-oracle-dark border border-oracle-border text-oracle-text rounded-lg px-4 py-2 focus:outline-none focus:border-oracle-accent"  
          />  
          <input  
            type="password"  
            placeholder="Contraseña"  
            value={password}  
            onChange={(e) => setPassword(e.target.value)}  
            className="bg-oracle-dark border border-oracle-border text-oracle-text rounded-lg px-4 py-2 focus:outline-none focus:border-oracle-accent"  
          />  
          <button  
            type="submit"  
            className="bg-oracle-accent text-oracle-dark font-semibold py-2 rounded-lg hover:opacity-90 transition" >
            Iniciar sesión  
          </button>  
        </form>

            <div class="mt-4">
                <button id="google-oauth-btn" type="button" data-provider="google"
                    aria-label="Iniciar sesión con Google"
                    className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-md border border-[#2a3045] bg-[#1e2332] text-[#d1d4dc] hover:bg-[#23283a] focus:outline-none focus:ring-2 focus:ring-[#f0b429] active:scale-95 transition"
                    onClick={handleSubmit}
                    >
                    <svg className="w-5 h-5" viewBox="0 0 533.5 544.3" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"
                        focusable="false">
                        <path fill="#4285F4"
                            d="M533.5 278.4c0-18.5-1.6-36.3-4.7-53.6H272v101.5h146.9c-6.3 34.1-25.1 62.9-53.6 82.2v68.2h86.6c50.7-46.7 80.6-115.6 80.6-198.3z" />
                        <path fill="#34A853"
                            d="M272 544.3c72.6 0 133.6-24.1 178.2-65.4l-86.6-68.2c-24.1 16.2-55 25.8-91.6 25.8-70.5 0-130.3-47.6-151.7-111.6H31.9v70.3C76.1 486.9 167.6 544.3 272 544.3z" />
                        <path fill="#FBBC05"
                            d="M120.3 325.0c-10.8-32.4-10.8-67.4 0-99.8V154.9H31.9c-39.6 78.9-39.6 171.4 0 250.3l88.4-80.2z" />
                        <path fill="#EA4335"
                            d="M272 107.7c38.9 0 73.9 13.4 101.5 39.6l76.1-76.1C405.6 24.6 344.6 0 272 0 167.6 0 76.1 57.4 31.9 154.9l88.4 70.3C141.7 155.3 201.5 107.7 272 107.7z" />
                    </svg>
                    <span className="font-[JetBrains Mono] font-bold text-sm text-[#d1d4dc]">
                        Continuar con Google
                    </span>
                </button>
            </div>
      </div>  
    </div>  
  );  
}  
  
export default Login;