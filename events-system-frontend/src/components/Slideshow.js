import React, { useEffect, useState } from 'react';
import './Slideshow.css';

const images = [
  require('../assets/alex-zamora-FU1KddSIIR4-unsplash.jpg'),
  require('../assets/eric-park-QbX8A8eHfzw-unsplash.jpg'),
  require('../assets/kyle-head-p6rNTdAPbuk-unsplash.jpg'),
  require('../assets/adam-whitlock-I9j8Rk-JYFM-unsplash.jpg'),
  require('../assets/arjan-de-jong-4jxcf0I3-Sw-unsplash.jpg')
];

const Slideshow = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 3000); // Change slide every 3 seconds

    return () => clearInterval(interval); // Cleanup the interval on component unmount
  }, []);

  return (
    <div className="slideshow-container">
      {images.map((image, index) => (
        <div
          key={index}
          className={`mySlides fade ${index === currentIndex ? 'active' : ''}`}
        >
          <img src={image} alt={`Slide ${index + 1}`} />
        </div>
      ))}
    </div>
  );
};

export default Slideshow;
