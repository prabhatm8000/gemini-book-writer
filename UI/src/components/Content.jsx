import React, { useReducer } from 'react'
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
            default:
                return state
        }
    }, {
        ideaForSummaryGen: null,
        globalLoading: false
    })
    return (
        <div id='content'>
            <GenerateIdeas selector={selector} dispatch={dispatch} />
            <GenerateSummary selector={selector} dispatch={dispatch} />
            <Output />
        </div>
    )
}

export default Content
