function checkForUpdate()
{
    if (window.applicationCache != undefined && window.applicationCache != null)
    {
        window.applicationCache.addEventListener('updateready', updateApplication);
    }
}
function updateApplication(event)
{
    if (window.applicationCache.status != 4) return;
    window.applicationCache.removeEventListener('updateready', updateApplication);
    window.applicationCache.swapCache();
    window.location.reload();
}