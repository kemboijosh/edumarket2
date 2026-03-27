import React from 'react';
import '../css/Aboutus.css'; // Import the CSS file

const AboutUs = () => {
  return (
    <div className="about-container">
      {/* Header Section */}
      <section className="about-header">
        <h1 className="about-title">About EduMarket</h1>
        <p className="about-subtitle">
          Empowering education through accessible and affordable learning materials.
        </p>
      </section>

      {/* Mission & Vision */}
      <section className="about-mission">
        <div className="mission-vision-container">
          <div className="mission-card">
            <h2 className="section-title">Our Mission</h2>
            <p className="about-paragraph">
              At EduMarket, we aim to provide affordable and accessible educational
              materials to students across the country, fostering learning and growth
              in every community.
            </p>
          </div>
          <div className="vision-card">
            <h2 className="section-title">Our Vision</h2>
            <p className="about-paragraph">
              To be the leading online marketplace for textbooks, stationery, and school supplies,
              empowering learners everywhere with quality resources at their fingertips.
            </p>
          </div>
        </div>
      </section>

      {/* Our Story */}
      <section className="about-story">
        <h2 className="section-title">Our Story</h2>
        <p className="about-paragraph">
          Founded in 2020, EduMarket started as a small initiative to address the challenges
          students face in accessing quality educational materials. What began as a local
          bookstore has evolved into a comprehensive online platform serving thousands of
          students nationwide. Our commitment to education drives everything we do.
        </p>
      </section>

      {/* Our Team */}
      <section className="about-team">
        <h2 className="section-title">Meet the Team</h2>
        <div className="team-grid">
          <div className="team-member">
            <img
              src="https://via.placeholder.com/150/4f46e5/ffffff?text=JD"
              alt="Jane Doe"
              className="team-image"
            />
            <h3 className="member-name">Jane Doe</h3>
            <p className="member-role">Founder & CEO</p>
            <p className="member-bio">
              Passionate about education and technology, Jane leads EduMarket with a vision
              to democratize access to learning resources.
            </p>
          </div>
          <div className="team-member">
            <img
              src="https://via.placeholder.com/150/059669/ffffff?text=JS"
              alt="John Smith"
              className="team-image"
            />
            <h3 className="member-name">John Smith</h3>
            <p className="member-role">Head of Operations</p>
            <p className="member-bio">
              With 10+ years in logistics, John ensures smooth delivery of educational
              materials to students across the country.
            </p>
          </div>
          <div className="team-member">
            <img
              src="https://via.placeholder.com/150/dc2626/ffffff?text=AS"
              alt="Alice Johnson"
              className="team-image"
            />
            <h3 className="member-name">Alice Johnson</h3>
            <p className="member-role">Customer Success Manager</p>
            <p className="member-bio">
              Alice works directly with schools and students to ensure they find the
              perfect educational resources for their needs.
            </p>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="about-why">
        <h2 className="section-title">Why Choose EduMarket?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📚</div>
            <h3>Wide Selection</h3>
            <p>Thousands of textbooks, stationery, and supplies from trusted publishers.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💰</div>
            <h3>Affordable Prices</h3>
            <p>Competitive pricing with frequent discounts and student-friendly deals.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🚚</div>
            <h3>Fast Delivery</h3>
            <p>Reliable shipping across the country with tracking and secure packaging.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⭐</div>
            <h3>Quality Assurance</h3>
            <p>All products are carefully inspected to ensure they meet our high standards.</p>
          </div>
        </div>
      </section>

      {/* Contact Info */}
      <section className="about-contact">
        <h2 className="section-title">Get in Touch</h2>
        <p className="about-paragraph">
          Have questions or want to collaborate? We'd love to hear from you!
        </p>
        <div className="contact-info">
          <div className="contact-item">
            <span className="contact-icon">📧</span>
            <a href="mailto:info@edumarket.com" className="email-link">info@edumarket.com</a>
          </div>
          <div className="contact-item">
            <span className="contact-icon">📞</span>
            <span>+1 (555) 123-4567</span>
          </div>
          <div className="contact-item">
            <span className="contact-icon">📍</span>
            <span>123 Education Street, Learning City, LC 12345</span>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutUs;