import React, { useState } from 'react'
import BookSummary from './BookSummary'

const styles = ["persuasive", "narrative", "expository", "descriptive"]

const GenerateSummary = ({ selector, dispatch, fetchFullBookChunkedJsonData }) => {
    const [creativity, setCreativity] = useState(7)
    const [logic, setLogic] = useState(7)
    const [noOfChapters, setNoOfChapters] = useState(5)

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError(null)
        setLoading(true)

        const title = e.target[0].value
        const style = e.target[1].value
        const description = e.target[2].value
        const genre = e.target[3].value

        if (!title || !style || !genre || !description) {
            setError('Please fill all the fields')
            setLoading(false)
            return
        }

        const response = await fetch('http://localhost:5000/api/generate-book-summary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                style,
                genre,
                description,
                creativity,
                logic,
                noOfChapters
            })
        })

        setLoading(false)
        const data = await response.json()

        if (!response.ok) {
            setError('Something went wrong')
        } else if ('error' in data) {
            setError(data.error)
        } else {
            dispatch({ type: 'setbookSummary', payload: data })
        }
    }

    const handleGenerateFullBook = () => {
        fetchFullBookChunkedJsonData()
    }

    return (
        <div className="content-container" id="generate-book-container">
            <h3>1. Generate a book with your ideas</h3>
            <div>
                <form
                    id="generate-book-form"
                    onSubmit={handleSubmit}
                >
                    <input
                        title="Title of the book"
                        className="inp1"
                        type="text"
                        name="title"
                        id="generate-summary-title-input"
                        placeholder="Enter title"
                        value={selector?.ideaForSummaryGen?.title || ""}
                    />
                    <select
                        name="style"
                        id="generate-summary-style-input"
                        className="inp1"
                        value={selector?.ideaForSummaryGen?.style || ""}
                    >
                        <option value="">Select style</option>
                        {styles.map((style) => (
                            <option key={style} value={style} style={{ textTransform: 'capitalize' }}>{style}</option>
                        ))}
                    </select>
                    <textarea
                        value={selector?.ideaForSummaryGen?.description || ""}
                        title="Description of the book"
                        className="inp1"
                        type="text"
                        name="description"
                        id="generate-summary-description-input"
                        placeholder="Enter description"
                        maxLength="480"
                    ></textarea>
                    <input
                        value={selector?.ideaForSummaryGen?.genre || ""}
                        title="Genre of the book"
                        className="inp1"
                        type="text"
                        name="genre"
                        id="generate-summary-genre-input"
                        placeholder="Enter genre followed by comma"
                    />
                    <input
                        value={noOfChapters}
                        onChange={e => setNoOfChapters(e.target.value)}
                        title="Number of chapters"
                        className="inp1"
                        type="number"
                        name="number-of-chapters"
                        id="generate-summary-chapters-input"
                        placeholder="Enter number of chapters"
                        min="1"
                        max="25"
                    />
                    <input
                        value={creativity}
                        onChange={e => setCreativity(e.target.value)}
                        title="Creativity of the book"
                        className="inp1"
                        type="number"
                        name="creativity"
                        id="generate-summary-creativity-input"
                        placeholder="Enter creativity level out of 10"
                        min="-10"
                        max="10"
                    />
                    <input
                        value={logic}
                        onChange={e => setLogic(e.target.value)}
                        title="Logic of the book"
                        className="inp1"
                        type="number"
                        name="logic"
                        id="generate-summary-logic-input"
                        placeholder="Enter logic level out of 10"
                        min="-10"
                        max="10"
                    />
                    <input
                        disabled={loading || selector?.globalLoading}
                        className="btn1"
                        type="submit"
                        value="Generate Summary"
                        id="generate-summary-btn"
                    />
                </form>
            </div>
            <div id="generated-summary">
                {!selector?.bookSummary && loading && <>waiting for response...</>}
                {error && <p className='error'>{error}</p>}
                {!error && selector?.bookSummary && <BookSummary bookSummary={selector.bookSummary} handleGenerateFullBook={handleGenerateFullBook} />}
            </div>
        </div>
    )
}

export default GenerateSummary
