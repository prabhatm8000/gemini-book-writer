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
        try {
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

            if (!response.ok) {
                setError("Something went wrong")
            }

            const data = await response.json()
            if ("error" in data) {
                setError(data.error)
            } else {
                setIdeas(data?.ideas)
            }
        } catch (error) {
            setError("Something went wrong")
            setIdeas([])
        }
        setLoading(false)
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
                    <div className='btn1 flex-gap-10'>
                        {
                            (loading || selector.globalLoading) ?
                                <svg className="loading-circle" width="18" height="18" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="#ffffff50" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                :
                                <input
                                    disabled={loading || selector.globalLoading}
                                    className="btn"
                                    type="submit"
                                    value="Generate Ideas"
                                    id="generate-idea-btn"
                                />
                        }
                    </div>
                </form>
            </div>

            <div id="generated-ideas" className={error ? 'error' : ''}>
                {loading && <>waiting for response...</>}
                {error && <p className='error'>{error}</p>}
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
