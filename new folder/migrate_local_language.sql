-- Migration script to add local language and dialect support
-- Run this script to update your existing database

USE cultural_corpus_platform;

-- Add new columns to cultural_items table for local language support
ALTER TABLE cultural_items 
ADD COLUMN local_language_name VARCHAR(500) NULL COMMENT 'Name in local language' AFTER location_name,
ADD COLUMN dialect_regional_variation VARCHAR(255) NULL COMMENT 'Dialect or regional variation' AFTER local_language_name,
ADD COLUMN pronunciation_guide VARCHAR(500) NULL COMMENT 'Pronunciation guide in English letters' AFTER dialect_regional_variation,
ADD COLUMN cultural_context VARCHAR(500) NULL COMMENT 'Cultural context and usage' AFTER pronunciation_guide,
ADD COLUMN local_language_audio_path VARCHAR(1000) NULL COMMENT 'Path to audio recording of pronunciation' AFTER cultural_context;

-- Create local_languages table
CREATE TABLE IF NOT EXISTS local_languages (
    language_id INT AUTO_INCREMENT PRIMARY KEY,
    language_name VARCHAR(255) NOT NULL,
    dialect_name VARCHAR(255) NULL,
    region VARCHAR(255) NULL,
    country VARCHAR(255) NULL,
    script_name VARCHAR(255) NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Add indexes for performance
CREATE INDEX idx_cultural_items_local_language ON cultural_items (local_language_name);
CREATE INDEX idx_cultural_items_dialect ON cultural_items (dialect_regional_variation);
CREATE INDEX idx_local_languages_name ON local_languages (language_name);
CREATE INDEX idx_local_languages_dialect ON local_languages (dialect_name);

-- Insert some common Indian languages and dialects
INSERT INTO local_languages (language_name, dialect_name, region, country, script_name) VALUES
('Telugu', 'Standard Telugu', 'Andhra Pradesh, Telangana', 'India', 'Telugu script'),
('Telugu', 'Hyderabad Telugu', 'Hyderabad, Telangana', 'India', 'Telugu script'),
('Telugu', 'Coastal Telugu', 'Coastal Andhra Pradesh', 'India', 'Telugu script'),
('Hindi', 'Standard Hindi', 'North India', 'India', 'Devanagari'),
('Hindi', 'Haryanvi', 'Haryana', 'India', 'Devanagari'),
('Hindi', 'Braj', 'Uttar Pradesh', 'India', 'Devanagari'),
('Bengali', 'Standard Bengali', 'West Bengal', 'India', 'Bengali script'),
('Bengali', 'Kolkata Bengali', 'Kolkata, West Bengal', 'India', 'Bengali script'),
('Bengali', 'Sylheti', 'Sylhet region', 'Bangladesh', 'Bengali script'),
('Tamil', 'Standard Tamil', 'Tamil Nadu', 'India', 'Tamil script'),
('Tamil', 'Chennai Tamil', 'Chennai, Tamil Nadu', 'India', 'Tamil script'),
('Kannada', 'Standard Kannada', 'Karnataka', 'India', 'Kannada script'),
('Kannada', 'Bangalore Kannada', 'Bangalore, Karnataka', 'India', 'Kannada script'),
('Malayalam', 'Standard Malayalam', 'Kerala', 'India', 'Malayalam script'),
('Malayalam', 'Thiruvananthapuram Malayalam', 'Thiruvananthapuram, Kerala', 'India', 'Malayalam script'),
('Marathi', 'Standard Marathi', 'Maharashtra', 'India', 'Devanagari'),
('Marathi', 'Mumbai Marathi', 'Mumbai, Maharashtra', 'India', 'Devanagari'),
('Gujarati', 'Standard Gujarati', 'Gujarat', 'India', 'Gujarati script'),
('Gujarati', 'Ahmedabad Gujarati', 'Ahmedabad, Gujarat', 'India', 'Gujarati script'),
('Punjabi', 'Standard Punjabi', 'Punjab', 'India', 'Gurmukhi'),
('Punjabi', 'Lahore Punjabi', 'Lahore, Pakistan', 'Pakistan', 'Shahmukhi'),
('Urdu', 'Standard Urdu', 'North India, Pakistan', 'India, Pakistan', 'Perso-Arabic'),
('Urdu', 'Hyderabad Urdu', 'Hyderabad, India', 'India', 'Perso-Arabic'),
('Odia', 'Standard Odia', 'Odisha', 'India', 'Odia script'),
('Assamese', 'Standard Assamese', 'Assam', 'India', 'Assamese script'),
('Sanskrit', 'Classical Sanskrit', 'Pan-India', 'India', 'Devanagari'),
('English', 'Indian English', 'Pan-India', 'India', 'Latin'),
('English', 'Hyderabad English', 'Hyderabad, India', 'India', 'Latin');

-- Update CSV file structure (if using CSV storage)
-- Note: The CSV file will be automatically updated when new submissions are made
-- with the new local language fields.

SELECT 'Migration completed successfully!' as status; 