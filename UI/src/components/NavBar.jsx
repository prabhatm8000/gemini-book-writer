import React from 'react'

export default function NavBar() {
    return (<div>
        <nav>
            <div>
                <img src="./gemini.svg" alt="gemini logo" width={50} height={50} />
                <h1>Gemini Book Writer</h1>
            </div>
            <div>
                <a
                    href="https://github.com/prabhatm8000/gemini-book-writer"
                    target="_blank"
                >Github
                </a>
                <a href="./readme.md">How to use?</a>
            </div>
        </nav>
    </div>)
}