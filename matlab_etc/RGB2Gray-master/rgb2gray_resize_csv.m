function rgb2gray_resize_csv(folder_path, row, col)
% Example
% rgb2gray_resize_csv('E:\190516\RGB2Gray', 28, 28);

    list = dir(folder_path);
    list = struct2cell(list(3:end, :));
    list = list(1, :);
    len = size(list, 2);
    
    for i = 1:len
        filename = cell2mat(list(i));
        
        if isempty(find((filename(end-3:end) == '.jpg')==false))
            img = imread([filename]);
            imgray = rgb2gray(img);
            imgrs = imresize(imgray, [row, col]);

            imgrs = vec2mat(imgrs, row*col);
            csvwrite(['grayimage_' int2str(i) '.csv'],imgrs);
        end
    end

end