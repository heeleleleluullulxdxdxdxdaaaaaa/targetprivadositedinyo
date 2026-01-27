
document.getElementById('fileInput').addEventListener('change', function(e) 
{
    const fileInputDiv = document.getElementById('fileInputDiv');
    if (this.files.length > 0) 
    {
        fileInputDiv.classList.add('success');
    } 
    else 
    {
        fileInputDiv.classList.remove('success');
    }
});

document.getElementById('myNumber').addEventListener('input', function(e) 
{
    if (e.target.value.includes('.')) 
    {
        const parts = e.target.value.split('.');
        if (parts[1].length > 2) 
        {
            parts[1] = parts[1].slice(0, 2);
            e.target.value = parts.join('.');
        }
    }
});