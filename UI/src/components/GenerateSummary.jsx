import React, { useEffect, useState } from 'react'
import BookSummary from './BookSummary'

const styles = ["persuasive", "narrative", "expository", "descriptive"]

const GenerateSummary = ({ selector, dispatch, fetchFullBookChunkedJsonData }) => {
    const [formData, setFormData] = useState({
        title: '',
        style: '',
        description: '',
        genre: '',
        creativity: 7,
        logic: 7,
        noOfChapters: 5
    })

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleFormInputChange = (name, value) => {
        setFormData(prev => { return { ...prev, [name]: value } })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        dispatch({ type: 'setbookSummary', payload: null })
        setError(null)
        setLoading(true)

        const { title, style, description, genre, creativity, logic, noOfChapters } = formData

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
        try {
            fetchFullBookChunkedJsonData()
        } catch (error) {
            dispatch({ type: 'setpollChapter', payload: false });
            dispatch({ type: 'setGlobalLoading', payload: false });
        }
    }

    useEffect(() => {
        if (!selector.ideaForSummaryGen) {
            return;
        }

        setFormData(prev => {
            const { title, style, description, genre } = selector?.ideaForSummaryGen;
            if (typeof genre === 'object') {
                return {
                    ...prev,
                    title: title || prev.title,
                    style: style || prev.style,
                    description: description || prev.description,
                    genre: genre.join(', ') || prev.genre
                }
            }

            return {
                ...prev,
                title: title || prev.title,
                style: style || prev.style,
                description: description || prev.description,
                genre: genre || prev.genre
            }
        })
    }, [selector.ideaForSummaryGen])

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
                        value={formData?.title || ""}
                        onChange={e => handleFormInputChange('title', e.target.value)}
                    />
                    <select
                        name="style"
                        id="generate-summary-style-input"
                        className="inp1"
                        value={formData?.style || ""}
                        onChange={e => handleFormInputChange('style', e.target.value)}
                    >
                        <option value="">Select style</option>
                        {styles.map((style) => (
                            <option key={style} value={style} style={{ textTransform: 'capitalize' }}>{style}</option>
                        ))}
                    </select>
                    <textarea
                        value={formData?.description || ""}
                        onChange={e => handleFormInputChange('description', e.target.value)}
                        title="Description of the book"
                        className="inp1"
                        type="text"
                        name="description"
                        id="generate-summary-description-input"
                        placeholder="Enter description"
                        maxLength="480"
                    ></textarea>
                    <input
                        value={formData?.genre || ""}
                        onChange={e => handleFormInputChange('genre', e.target.value)}
                        title="Genre of the book"
                        className="inp1"
                        type="text"
                        name="genre"
                        id="generate-summary-genre-input"
                        placeholder="Enter genre followed by comma"
                    />
                    <input
                        value={formData?.noOfChapters || ""}
                        onChange={e => handleFormInputChange('noOfChapters', e.target.value)}
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
                        value={formData?.creativity || ""}
                        onChange={e => handleFormInputChange('creativity', e.target.value)}
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
                        value={formData?.logic || ""}
                        onChange={e => handleFormInputChange('logic', e.target.value)}
                        title="Logic of the book"
                        className="inp1"
                        type="number"
                        name="logic"
                        id="generate-summary-logic-input"
                        placeholder="Enter logic level out of 10"
                        min="-10"
                        max="10"
                    />
                    <button
                        disabled={loading || selector?.globalLoading}
                        className="btn1 flex-gap-10"
                        type="submit"
                        value="Generate Summary"
                        id="generate-summary-btn"
                    >
                        <span>
                            Generate Summary
                        </span>
                        {
                            (loading || selector.globalLoading) &&
                            <svg className="loading-circle" width="18" height="18" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="#ffffff50" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        }
                    </button>

                </form>
            </div>
            <div id="generated-summary">
                {!selector?.bookSummary && loading && <>waiting for response...</>}
                {error && <p className='error'>{error}</p>}
                {!error && selector?.bookSummary && <BookSummary loading={loading || selector?.globalLoading} bookSummary={selector.bookSummary} handleGenerateFullBook={handleGenerateFullBook} />}
            </div>
        </div>
    )
}

export default GenerateSummary
