import React, { useEffect, useReducer } from 'react'
import GenerateIdeas from './GenerateIdeas'
import Output from './Output'
import GenerateSummary from './GenerateSummary'

const Content = () => {
    const [selector, dispatch] = useReducer((state, action) => {
        switch (action.type) {
            case 'setideaForSummaryGen':
                return { ...state, ideaForSummaryGen: action.payload }
            case 'setGlobalLoading':
                return { ...state, globalLoading: action.payload }
            case 'setpollChapter':
                return { ...state, pollChapter: action.payload }
            case 'setbookSummary':
                return { ...state, bookSummary: action.payload }
            case 'resetChapters':
                return { ...state, chapters: [] }
            case 'appendChapter':
                return { ...state, chapters: [...state.chapters, action.payload] }
            case 'seterror':
                return { ...state, error: action.payload }
            default:
                return state
        }
    }, {
        ideaForSummaryGen: null,
        globalLoading: false,
        pollChapter: false,
        bookSummary: null,
        chapters: [],
        error: null
    })

    useEffect(() => {
        if (selector.chapters.length > 0) {
            document.title = `${selector.bookSummary?.title || "Book"}`
        } else {
            document.title = "Gemini Writer"
        }
    }, [selector])

    async function fetchFullBookChunkedJsonData() {
        dispatch({ type: 'seterror', payload: null });
        dispatch({ type: 'setpollChapter', payload: true });
        dispatch({ type: 'setGlobalLoading', payload: true });
        dispatch({ type: 'resetChapters' });

        const response = await fetch('http://localhost:5000/api/generate-full-book');
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let { done, value } = await reader.read();
        let accumulator = "";

        while (!done) {
            const chunkText = decoder.decode(value, { stream: true });
            accumulator += chunkText;

            if (chunkText.startsWith(`{"error":`)) {
                const jsonData = JSON.parse(chunkText);
                dispatch({ type: 'seterror', payload: jsonData });
                console.log(jsonData);
                break;
            }

            if (!accumulator.includes(`"]}`)) {
                ({ done, value } = await reader.read());
                continue;
            }

            const texts = accumulator.split(`"]}`);
            const textToParse = texts[0] + `"]}`;
            accumulator = texts[1];

            try {
                const jsonData = JSON.parse(textToParse);
                dispatch({ type: 'appendChapter', payload: jsonData });
            } catch (e) {
                console.error('Failed to parse JSON:');
                dispatch({ type: 'setpollChapter', payload: false });
                dispatch({ type: 'setGlobalLoading', payload: false });
            }
            ({ done, value } = await reader.read());
        }

        dispatch({ type: 'seterror', payload: null });
        dispatch({ type: 'setpollChapter', payload: false });
        dispatch({ type: 'setGlobalLoading', payload: false });
    }

    return (
        <div id='content'>
            <GenerateIdeas selector={selector} dispatch={dispatch} />
            <GenerateSummary selector={selector} dispatch={dispatch} fetchFullBookChunkedJsonData={fetchFullBookChunkedJsonData} />
            <Output selector={selector} dispatch={dispatch} />
        </div>
    )
}

export default Content
