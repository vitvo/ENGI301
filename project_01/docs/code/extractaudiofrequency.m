%Vi Vo 
%Last Modified October 12th, 2020
%Obtaining the frequency of each of the asteroids sound to play on 
%Piezzo buzzer using Matlab Audio Toolbox.

for audio = 1:4
    audioFile = getfield(dir('*.ogg'),{audio}, 'name');
    [audioIn, fs] = audioread(audioFile);
    frequency.(erase(audioFile,'.ogg')) = pitch(audioIn, fs);
end
clearvars -except frequency