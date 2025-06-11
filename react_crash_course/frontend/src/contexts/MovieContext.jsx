import { createContext, useState, useContext, useEffect } from "react";

// MovieContext
const MovieContext = createContext()

// useMovieContext -> gets called when there is a change in favorites... 
// and updates moviecontext

export const useMovieContext = () => useContext(MovieContext)
// export const useMovieContext = () => useContext(MovieContext)

// note that children is a reserved prop
export const MovieProvider = ({children}) => {
    const [favorites, setFavorites] = useState([])

    useEffect(() => {
        // setFavorites : localstorage setitem, getitem
        const storedFavs = localStorage.getItem("favorites")

        if(storedFavs) setFavorites(JSON.parse(storedFavs))
        
    }, [])
        
    useEffect(() => {
        localStorage.setItem('favorites', JSON.stringify(favorites))
    }, [favorites])

    // addtofav, removefromfav, isfavorite
    const addToFavorites = (movie) => {
        setFavorites(prev => [...prev, movie])
    }

    const removeFromFavorites = (movieId) => {
        setFavorites(prev => prev.filter(movie => movie.id !== movieId))
    }

    const isFavorite = (movieId) => {
        return favorites.some(movie => movie.id === movieId)
    }

    // value containing favorites, addtofav, removefromfav, isfav

    const value = {
        favorites,
        addToFavorites,
        removeFromFavorites,
        isFavorite
    }

    // not typing .provider since documentation says no need, experimenting
    return <MovieContext value={value}>
        {children}
    </MovieContext>
}
