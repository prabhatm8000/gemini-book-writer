import React, { useState } from 'react'
import IdeaCard from './IdeaCard'

const GenerateIdeas = ({ selector, dispatch }) => {
    const [loading, setLoading] = useState(false)
    const [ideas, setIdeas] = useState([])
    const [error, setError] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()

        const prompt = e.target[0].value
        const limit = e.target[1].value

        if (!prompt || !limit) {
            return
        }

        setError(null)
        setLoading(true)
        const response = await fetch('http://localhost:5000/api/generate-book-ideas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt,
                limit
            })
        })
        setLoading(false)

        if (!response.ok) {
            const data = await response.json()
            setError(data.error)
        } else {
            const data = await response.json()
            if (Array.isArray(data?.ideas)) {
                setIdeas(data?.ideas)
            } else {
                setError(`${data}`)
            }
        }
    }

    const handleGenerateChaptersBtn = (index) => {
        const idea = ideas[index]
        dispatch({ type: 'setideaForSummaryGen', payload: { ...idea, style: idea?.style.toLowerCase() } })
    }

    return (
        <div className="content-container" id="generate-idea-container">
            <h3>0. Generate ideas for your book</h3>
            <div>
                <form
                    id="generate-idea-form"
                    onSubmit={handleSubmit}
                >
                    <textarea
                        title="Prompt for ideas"
                        className="inp1"
                        type="text"
                        name="prompt"
                        id="prompt"
                        placeholder="Enter prompt"
                    ></textarea>
                    <input
                        title="Number of ideas"
                        className="inp1"
                        type="number"
                        name="limit"
                        id="limit"
                        placeholder="Enter limit"
                        min="1"
                        max="10"
                    />
                    <input
                        disabled={loading || selector?.globalLoading}
                        className="btn1"
                        type="submit"
                        value="Generate Ideas"
                        id="generate-idea-btn"
                    />
                </form>
            </div>

            <div id="generated-ideas" className={error ? 'error' : ''}>
                {loading && <>waiting for response...</>}
                {error && <>Error: {error}</>}
                {ideas.length > 0 && (
                    ideas.map((item, index) => {
                        return (
                            <IdeaCard
                                key={index}
                                idea={item}
                                handleGenerateChaptersBtn={handleGenerateChaptersBtn}
                                index={index}
                                selector={selector}
                                loading={loading}
                            />
                        )
                    })
                )}
            </div>
        </div>
    )
}

export default GenerateIdeas
